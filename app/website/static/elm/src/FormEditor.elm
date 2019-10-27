module FormEditor exposing (..)

import Browser
import FieldEditor exposing (..)
import Html exposing (..)
import Html.Attributes exposing (..)
import Html.Events exposing (..)
import Http exposing (..)
import Json.Decode as JD
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


type alias IndexedField =
    { idx : Int
    , field : FieldEditor.Model
    }


type alias Model =
    { name : String
    , title : String
    , description : String
    , fields : List IndexedField
    , nextIdx : Int
    }


init : () -> ( Model, Cmd Msg )
init _ =
    let
        fieldList : List IndexedField
        fieldList =
            [ { idx = 0
              , field =
                    { question = "Untitled Question"
                    , description = ""
                    , answerMethod = defaultAnswerMethod
                    , required = False
                    , expanded = True
                    }
              }
            ]
    in
    ( { name = "Untitled Form"
      , title = "Untitled Form"
      , description = ""
      , fields = fieldList
      , nextIdx = List.length fieldList
      }
    , Cmd.none
    )



-- UPDATE


type Msg
    = ChangeName String
    | ChangeTitle String
    | ChangeDescription String
    | AddField Int
    | DuplicateField IndexedField
    | DeleteField Int
    | ModifyField Int FieldMsg


update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        ChangeName name ->
            ( { model | name = name }
            , Cmd.none
            )

        ChangeTitle title ->
            ( { model | title = title }
            , Cmd.none
            )

        ChangeDescription description ->
            ( { model | description = description }
            , Cmd.none
            )

        AddField idx ->
            let
                newField : IndexedField
                newField =
                    { idx = idx
                    , field =
                        { question = ""
                        , description = ""
                        , answerMethod = defaultAnswerMethod
                        , required = False
                        , expanded = False
                        }
                    }
            in
            ( { model
                | fields = List.map (switchFocus newField.idx) (insertField newField model.fields)
                , nextIdx = model.nextIdx + 1
              }
            , Cmd.none
            )

        DuplicateField activeField ->
            let
                newField : IndexedField
                newField =
                    { activeField | idx = activeField.idx + 1 }
            in
            ( { model
                | fields = List.map (switchFocus newField.idx) (insertField newField model.fields)
                , nextIdx = model.nextIdx + 1
              }
            , Cmd.none
            )

        DeleteField idx ->
            ( { model
                | fields = List.map (switchFocus (idx - 1)) (deleteField idx model.fields)
                , nextIdx = model.nextIdx - 1
              }
            , Cmd.none
            )

        ModifyField idx msg_ ->
            case msg_ of
                Expand ->
                    ( { model | fields = List.map (switchFocus idx) model.fields }
                    , Cmd.none
                    )

                _ ->
                    ( { model | fields = List.map (modifyField idx msg_) model.fields }
                    , Cmd.none
                    )


switchFocus : Int -> IndexedField -> IndexedField
switchFocus targetIdx { idx, field } =
    IndexedField
        idx
        (if targetIdx == idx then
            let
                _ =
                    Debug.log "Idx " idx
            in
            updateField Expand field

         else
            updateField Collapse field
        )


modifyField : Int -> FieldMsg -> IndexedField -> IndexedField
modifyField targetIdx msg { idx, field } =
    IndexedField
        idx
        (if targetIdx == idx then
            updateField msg field

         else
            field
        )


insertField : IndexedField -> List IndexedField -> List IndexedField
insertField field fieldList =
    let
        before : List IndexedField
        before =
            List.take field.idx fieldList

        after : List IndexedField
        after =
            List.map (\x -> { x | idx = x.idx + 1 }) (List.drop field.idx fieldList)
    in
    before ++ field :: after


deleteField : Int -> List IndexedField -> List IndexedField
deleteField idx fieldList =
    let
        before : List IndexedField
        before =
            List.take idx fieldList

        after : List IndexedField
        after =
            List.map (\x -> { x | idx = x.idx - 1 }) (List.drop (idx + 1) fieldList)
    in
    before ++ after



-- VIEW


view : Model -> Html Msg
view model =
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
                , style "justify-content" "center"
                , style "align-content" "center"
                , style "padding" "1rem"
                , onInput ChangeName
                ]
                [ input
                    [ value model.name
                    ]
                    []
                , viewAddFieldButton (getActiveFieldIndex model.fields + 1)
                ]

        titleField : Html Msg
        titleField =
            div
                [ style "padding" "1rem"
                , onClick (ModifyField -1 Expand)
                ]
                [ viewQuestion model.title ChangeTitle
                , viewDescription model.description ChangeDescription
                ]

        fieldList : Html Msg
        fieldList =
            div
                [ style "margin-top" "2rem"
                ]
                ([ fieldWrapper titleField ] ++ List.map viewIndexedField model.fields)
    in
    div
        []
        [ formNavBar
        , fieldList
        ]


getActiveFieldIndex : List IndexedField -> Int
getActiveFieldIndex fieldList =
    let
        activeField : Maybe IndexedField
        activeField =
            List.head (List.filter (\x -> x.field.expanded) fieldList)
    in
    case activeField of
        Nothing ->
            List.length fieldList - 1

        Just { idx, field } ->
            idx


viewIndexedField : IndexedField -> Html Msg
viewIndexedField { idx, field } =
    let
        fieldQuestion : Html Msg
        fieldQuestion =
            viewQuestion field.question (ModifyField idx << ChangeQuestion)

        fieldAnswerMethod : Html Msg
        fieldAnswerMethod =
            viewAnswerMethod field.answerMethod
                field.expanded
                (ModifyField idx ToggleMenu)
                (ModifyField idx << ChangeAnswerMethod)

        fieldDescription : Html Msg
        fieldDescription =
            viewDescription field.description (ModifyField idx << FieldEditor.ChangeDescription)

        footerControls : Html Msg
        footerControls =
            div []
                [ viewDuplicateFieldButton (IndexedField idx field)
                , viewDeleteFieldButton idx
                ]

        fieldBody : Html Msg
        fieldBody =
            div
                []
                [ div
                    [ onClick (ModifyField idx Expand)
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
                        (ModifyField idx << ChangeRequired)
                        footerControls
                    )
                ]

        --            Html.map (ModifyField idx) (viewField field)
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


viewAddFieldButton : Int -> Html Msg
viewAddFieldButton idx =
    button [ onClick (AddField idx) ] [ text "Add Field" ]


viewDeleteFieldButton : Int -> Html Msg
viewDeleteFieldButton idx =
    button [ onClick (DeleteField idx) ] [ text "Delete" ]


viewDuplicateFieldButton : IndexedField -> Html Msg
viewDuplicateFieldButton field =
    button [ onClick (DuplicateField field) ] [ text "Duplicate" ]
