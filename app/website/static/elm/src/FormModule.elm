module FormModule exposing (..)

import Browser
import FieldModule as FE exposing (..)
import HTTP exposing (..)
import Html exposing (..)
import Html.Attributes exposing (..)
import Html.Events exposing (..)
import Http exposing (jsonBody)
import JSON exposing (..)
import MODEL exposing (..)
import Utils exposing (..)



-- MAIN


main =
    Browser.element
        { init = init
        , update = update
        , subscriptions = \_ -> Sub.none
        , view = view
        }



-- INIT


type alias MainInfo r =
    { r
        | name : String
        , title : String
        , description : String
    }


init : () -> ( Form, Cmd Msg )
init _ =
    let
        fieldList : List Field
        fieldList =
            [ { id = ""
              , rootId = ""
              , index = 0
              , question = "Untitled Question"
              , description = ""
              , answerMethod = defaultAnswerMethod
              , required = False
              , expanded = True
              , status = Loading
              }
            ]
    in
    ( { id = ""
      , name = "Untitled Form"
      , title = "Untitled Form"
      , description = ""
      , fields = fieldList
      , status = Loading
      }
    , getFormTemplate (rootURL ++ "5db76d95e22235367394f83c") GotForm
    )



-- UPDATE


type Msg
    = ChangeName String
    | ChangeTitle String
    | ChangeDescription String
    | AddField Field
    | DuplicateField Field
    | DeleteField Field
    | ModifyField Field FieldMsg
    | GotForm (Result Http.Error Form)


update : Msg -> Form -> ( Form, Cmd Msg )
update msg model =
    case msg of
        ChangeName name ->
            let
                newModel : Form
                newModel =
                    { model
                        | name = name
                        , status = Loading
                    }
            in
            ( newModel
            , (jsonBody (formMainInfoEncoder newModel)
                |> sendFormTemplate (rootURL ++ newModel.id)
              )
              <|
                GotForm
            )

        ChangeTitle title ->
            let
                newModel : Form
                newModel =
                    { model
                        | title = title
                        , status = Loading
                    }
            in
            ( newModel
            , (jsonBody (formMainInfoEncoder newModel)
                |> sendFormTemplate (rootURL ++ newModel.id)
              )
              <|
                GotForm
            )

        ChangeDescription description ->
            let
                newModel : Form
                newModel =
                    { model
                        | description = description
                        , status = Loading
                    }
            in
            ( newModel
            , (jsonBody (formMainInfoEncoder newModel)
                |> sendFormTemplate (rootURL ++ newModel.id)
              )
              <|
                GotForm
            )

        AddField activeField ->
            let
                newField : Field
                newField =
                    { id = ""
                    , rootId = model.id
                    , index = activeField.index + 1
                    , question = ""
                    , description = ""
                    , answerMethod = defaultAnswerMethod
                    , required = False
                    , expanded = True
                    , status = Loading
                    }
            in
            ( { model
                | fields = List.map (switchFocus newField.index) (insertField newField model.fields)
              }
            , (jsonBody (fieldEncoder newField)
                |> sendFormTemplate (rootURL ++ model.id ++ "/add/" ++ newField.id)
              )
              <|
                GotForm
            )

        DuplicateField activeField ->
            let
                newField : Field
                newField =
                    { activeField | index = activeField.index + 1 }
            in
            ( { model
                | fields = List.map (switchFocus newField.index) (insertField newField model.fields)
              }
            , (jsonBody (fieldEncoder newField)
                |> sendFormTemplate (rootURL ++ model.id ++ "/duplicate/" ++ activeField.id)
              )
              <|
                GotForm
            )

        DeleteField activeField ->
            ( { model
                | fields =
                    List.map (switchFocus (activeField.index - 1))
                        (deleteField activeField.index model.fields)
              }
            , (jsonBody (fieldEncoder activeField)
                |> sendFormTemplate (rootURL ++ model.id ++ "/delete/" ++ activeField.id)
              )
              <|
                GotForm
            )

        ModifyField activeField msg_ ->
            case msg_ of
                Expand ->
                    ( { model | fields = List.map (switchFocus activeField.index) model.fields }
                    , Cmd.none
                    )

                _ ->
                    ( { model | fields = List.map (modifyField activeField.id msg_) model.fields }
                    , Cmd.none
                    )

        GotForm result ->
            case result of
                Ok form ->
                    ( form, Cmd.none )

                Err err ->
                    let
                        _ =
                            case err of
                                Http.BadUrl bad ->
                                    Debug.log "BadUrl" bad

                                Http.Timeout ->
                                    Debug.log "Timeout" ""

                                Http.NetworkError ->
                                    Debug.log "NetworkError" ""

                                Http.BadStatus bad ->
                                    Debug.log "BadStatus" String.fromInt bad

                                Http.BadBody bad ->
                                    Debug.log "BadBody" bad
                    in
                    ( { model | status = Failure }
                    , Cmd.none
                    )


switchFocus : Int -> Field -> Field
switchFocus targetIdx field =
    let
        ( fld, _ ) =
            if targetIdx == field.index then
                updateField Expand field

            else
                updateField Collapse field
    in
    fld


modifyField : String -> FieldMsg -> Field -> Field
modifyField targetId msg field =
    let
        ( fld, _ ) =
            if targetId == field.id then
                updateField msg field

            else
                updateField DoNothing field
    in
    fld


insertField : Field -> List Field -> List Field
insertField field fieldList =
    let
        before : List Field
        before =
            List.take field.index fieldList

        after : List Field
        after =
            List.drop field.index fieldList
                |> List.map (\x -> { x | index = x.index + 1 })
    in
    before ++ field :: after


deleteField : Int -> List Field -> List Field
deleteField idx fieldList =
    let
        before : List Field
        before =
            List.take idx fieldList

        after : List Field
        after =
            List.drop (idx + 1) fieldList
                |> List.map (\x -> { x | index = x.index - 1 })
    in
    before ++ after


getActiveField : List Field -> Maybe Field
getActiveField fieldList =
    List.filter (\x -> x.expanded) fieldList
        |> List.head



-- VIEW


view : Form -> Html Msg
view model =
    viewForm model


viewForm : Form -> Html Msg
viewForm model =
    let
        formNavBar : Html Msg
        formNavBar =
            div
                [ style "background-color" "rgb(225, 225, 225)"
                , style "height" "2rem"
                , style "border-radius" "0.5rem"
                , style "position" "sticky"
                , style "top" "0.5rem"
                , style "display" "flex"
                , style "justify-content" "right"
                , style "align-content" "center"
                , style "padding" "1rem"
                , style "margin-bottom" "2rem"
                , onChange ChangeName
                ]
                [ input
                    [ value model.name
                    ]
                    []
                , viewAddFieldButton (getActiveField model.fields)
                , p [ style "margin-left" "2rem" ]
                    [ case model.status of
                        Loading ->
                            text "Saving..."

                        Success ->
                            text "Up to date."

                        Failure ->
                            text "Something went wrong!"
                    ]
                ]

        titleField : Html Msg
        titleField =
            div
                [ style "padding" "1rem"

                --                , onClick (ModifyField -1 Expand)
                ]
                [ viewQuestion model.title ChangeTitle
                , viewDescription model.description ChangeDescription
                ]

        fieldList : Html Msg
        fieldList =
            div
                []
                (List.map viewField model.fields)
    in
    div
        []
        [ formNavBar
        , fieldWrapper titleField
        , fieldList
        ]


viewField : Field -> Html Msg
viewField field =
    let
        fieldQuestion : Html Msg
        fieldQuestion =
            viewQuestion field.question (ModifyField field << ChangeQuestion)

        fieldAnswerMethod : Html Msg
        fieldAnswerMethod =
            viewAnswerMethod field.answerMethod
                field.expanded
                (ModifyField field ToggleMenu)
                (ModifyField field << ChangeAnswerMethod)

        fieldDescription : Html Msg
        fieldDescription =
            ModifyField field
                << FE.ChangeDescription
                |> viewDescription field.description

        footerControls : Html Msg
        footerControls =
            div []
                [ viewDuplicateFieldButton field
                , viewDeleteFieldButton field
                ]

        fieldBody : Html Msg
        fieldBody =
            div
                []
                [ div
                    [ onClick (ModifyField field Expand)
                    , style "padding" "1rem"
                    ]
                    [ div
                        [ style "display" "flex"
                        , style "justify-content" "center"
                        ]
                        [ fieldQuestion
                        , fieldAnswerMethod
                        ]
                    , fieldDescription
                    ]
                , viewControls field
                    (fieldFooter field
                        (ModifyField field << ChangeRequired)
                        footerControls
                    )
                ]
    in
    fieldWrapper fieldBody


fieldWrapper : Html msg -> Html msg
fieldWrapper content =
    div
        [ style "display" "flex"
        , style "justify-content" "center"
        , style "margin-bottom" "1rem"
        ]
        [ div
            [ style "width" "50rem"
            , style "border" "1px solid gray"
            , style "border-radius" "0.5rem"
            ]
            [ content
            ]
        ]


viewAddFieldButton : Maybe Field -> Html Msg
viewAddFieldButton maybeField =
    case maybeField of
        Nothing ->
            button [] [ text "Add Field" ]

        Just field ->
            button [ onClick (AddField field) ] [ text "Add Field" ]


viewDeleteFieldButton : Field -> Html Msg
viewDeleteFieldButton field =
    button [ onClick (DeleteField field) ] [ text "Delete" ]


viewDuplicateFieldButton : Field -> Html Msg
viewDuplicateFieldButton field =
    button [ onClick (DuplicateField field) ] [ text "Duplicate" ]
