module FormEditor exposing (..)

import Browser
import FieldEditor as FE exposing (..)
import Html exposing (..)
import Html.Attributes exposing (..)
import Html.Events exposing (..)
import Http exposing (Body, jsonBody)
import Json.Decode as JD exposing (Decoder, list, string)
import Json.Decode.Pipeline as JDP exposing (hardcoded, required)
import Json.Encode as JE



-- MAIN


main =
    Browser.element
        { init = init
        , update = update
        , subscriptions = \_ -> Sub.none
        , view = view
        }



-- MODEL


type FormStatus
    = Loading
    | Success
    | Failure


type alias Model =
    { id : String
    , name : String
    , title : String
    , description : String
    , fields : List FE.Model
    , status : FormStatus
    }


type alias MainInfo r =
    { r
        | name : String
        , title : String
        , description : String
    }


init : () -> ( Model, Cmd Msg )
init _ =
    let
        fieldList : List FE.Model
        fieldList =
            [ { id = ""
              , index = 0
              , question = "Untitled Question"
              , description = ""
              , answerMethod = defaultAnswerMethod
              , required = False
              , expanded = True
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
    , getFormTemplate (rootURL ++ "5db76d95e22235367394f83c")
    )


rootURL : String
rootURL =
    "http://127.0.0.1:5000/forms-json/"



-- UPDATE


type Msg
    = ChangeName String
    | ChangeTitle String
    | ChangeDescription String
    | AddField FE.Model
    | DuplicateField FE.Model
    | DeleteField FE.Model
    | ModifyField FE.Model FieldMsg
    | GotForm (Result Http.Error Model)


update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        ChangeName name ->
            let
                newModel =
                    { model
                        | name = name
                        , status = Loading
                    }
            in
            ( newModel
            , jsonBody (formMainInfoEncoder newModel)
                |> sendFormTemplate (rootURL ++ newModel.id)
            )

        ChangeTitle title ->
            let
                newModel =
                    { model
                        | title = title
                        , status = Loading
                    }
            in
            ( newModel
            , jsonBody (formMainInfoEncoder newModel)
                |> sendFormTemplate (rootURL ++ newModel.id)
            )

        ChangeDescription description ->
            let
                newModel =
                    { model
                        | description = description
                        , status = Loading
                    }
            in
            ( newModel
            , jsonBody (formMainInfoEncoder newModel)
                |> sendFormTemplate (rootURL ++ newModel.id)
            )

        AddField activeField ->
            let
                newField : FE.Model
                newField =
                    { id = ""
                    , index = activeField.index
                    , question = ""
                    , description = ""
                    , answerMethod = defaultAnswerMethod
                    , required = False
                    , expanded = True
                    }
            in
            ( { model
                | fields = List.map (switchFocus newField.index) (insertField newField model.fields)
              }
            , jsonBody (fieldEncoder newField)
                |> sendFormTemplate (rootURL ++ model.id ++ "/add/" ++ newField.id)
            )

        DuplicateField activeField ->
            let
                newField : FE.Model
                newField =
                    { activeField | index = activeField.index + 1 }
            in
            ( { model
                | fields = List.map (switchFocus newField.index) (insertField newField model.fields)
              }
            , jsonBody (fieldEncoder newField)
                |> sendFormTemplate (rootURL ++ model.id ++ "/duplicate/" ++ activeField.id)
            )

        DeleteField activeField ->
            ( { model
                | fields =
                    List.map (switchFocus (activeField.index - 1))
                        (deleteField activeField.index model.fields)
              }
            , jsonBody (fieldEncoder activeField)
                |> sendFormTemplate (rootURL ++ model.id ++ "/delete/" ++ activeField.id)
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


switchFocus : Int -> FE.Model -> FE.Model
switchFocus targetIdx field =
    if targetIdx == field.index then
        updateField Expand field

    else
        updateField Collapse field


modifyField : String -> FieldMsg -> FE.Model -> FE.Model
modifyField targetId msg field =
    if targetId == field.id then
        updateField msg field

    else
        field


insertField : FE.Model -> List FE.Model -> List FE.Model
insertField field fieldList =
    let
        before : List FE.Model
        before =
            List.take field.index fieldList

        after : List FE.Model
        after =
            List.drop field.index fieldList
                |> List.map (\x -> { x | index = x.index + 1 })
    in
    before ++ field :: after


deleteField : Int -> List FE.Model -> List FE.Model
deleteField idx fieldList =
    let
        before : List FE.Model
        before =
            List.take idx fieldList

        after : List FE.Model
        after =
            List.drop (idx + 1) fieldList
                |> List.map (\x -> { x | index = x.index - 1 })
    in
    before ++ after


getActiveField : List FE.Model -> Maybe FE.Model
getActiveField fieldList =
    List.filter (\x -> x.expanded) fieldList
        |> List.head



-- VIEW


view : Model -> Html Msg
view model =
    viewForm model


viewForm : Model -> Html Msg
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
                , onInput ChangeName
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


viewField : FE.Model -> Html Msg
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


viewAddFieldButton : Maybe FE.Model -> Html Msg
viewAddFieldButton maybeField =
    case maybeField of
        Nothing ->
            button [] [ text "Add Field" ]

        Just field ->
            button [ onClick (AddField field) ] [ text "Add Field" ]


viewDeleteFieldButton : FE.Model -> Html Msg
viewDeleteFieldButton field =
    button [ onClick (DeleteField field) ] [ text "Delete" ]


viewDuplicateFieldButton : FE.Model -> Html Msg
viewDuplicateFieldButton field =
    button [ onClick (DuplicateField field) ] [ text "Duplicate" ]



-- HTTP


getFormTemplate : String -> Cmd Msg
getFormTemplate url =
    Http.get
        { url = url
        , expect = Http.expectJson GotForm formDecoder
        }


sendFormTemplate : String -> Http.Body -> Cmd Msg
sendFormTemplate url data =
    Http.post
        { url = url
        , body = data
        , expect = Http.expectJson GotForm formDecoder
        }



-- JSON


formMainInfoEncoder : Model -> JE.Value
formMainInfoEncoder form =
    JE.object
        [ ( "name", JE.string form.name )
        , ( "title", JE.string form.title )
        , ( "description", JE.string form.description )
        ]


formDecoder : JD.Decoder Model
formDecoder =
    JD.succeed Model
        |> required "_id" string
        |> required "name" string
        |> required "title" string
        |> required "description" string
        |> required "fields" (list fieldDecoder)
        |> hardcoded Success
