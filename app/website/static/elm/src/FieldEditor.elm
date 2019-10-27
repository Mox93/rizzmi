module FieldEditor exposing (..)

import Browser
import Html exposing (..)
import Html.Attributes exposing (..)
import Html.Events exposing (..)



-- MAIN


main =
    Browser.sandbox
        { init = init
        , update = updateField
        , view = viewField
        }



-- MODEL


type AnswerMethod
    = ShortAnswer
    | Paragraph
    | MultipleChoice
    | CheckBox
    | DropDown


type alias SelectedAnswerMethod =
    { selected : AnswerMethod
    , menuOpen : Bool
    }


type alias Model =
    { question : String
    , description : String
    , answerMethod : SelectedAnswerMethod
    , required : Bool
    , expanded : Bool
    }


defaultAnswerMethod : SelectedAnswerMethod
defaultAnswerMethod =
    SelectedAnswerMethod ShortAnswer False


init : Model
init =
    { question = "Test Field"
    , description = "This is some text to fill in the description are"
    , answerMethod = defaultAnswerMethod
    , required = False
    , expanded = False
    }



-- UPDATE


type FieldMsg
    = Expand
    | Collapse
    | ChangeAnswerMethod AnswerMethod
    | ToggleMenu
    | ChangeRequired Bool
    | ChangeQuestion String
    | ChangeDescription String
    | DoNothing


updateField : FieldMsg -> Model -> Model
updateField msg model =
    case msg of
        Expand ->
            { model | expanded = True }

        Collapse ->
            let
                menu : SelectedAnswerMethod
                menu =
                    model.answerMethod
            in
            { model
                | expanded = False
                , answerMethod = { menu | menuOpen = False }
            }

        ChangeAnswerMethod method ->
            let
                menu =
                    model.answerMethod
            in
            { model | answerMethod = { menu | selected = method } }

        ToggleMenu ->
            let
                menu =
                    model.answerMethod
            in
            { model | answerMethod = { menu | menuOpen = not menu.menuOpen } }

        ChangeRequired state ->
            { model | required = state }

        ChangeQuestion question ->
            { model | question = question }

        ChangeDescription description ->
            { model | description = description }

        DoNothing ->
            model



-- VIEW


viewField : Model -> Html FieldMsg
viewField model =
    div
        []
        [ div [ onClick Expand ]
            [ div
                [ style "display" "flex"
                , style "justify-content" "center"
                ]
                [ viewQuestion model.question ChangeQuestion
                , viewAnswerMethod model.answerMethod model.expanded ToggleMenu ChangeAnswerMethod
                ]
            , viewDescription model.description ChangeDescription
            ]
        , viewControls model (fieldFooter model ChangeRequired (div [] []))
        ]


viewQuestion : String -> (String -> msg) -> Html msg
viewQuestion question changeText =
    input
        [ placeholder "Question"
        , value question
        , style "width" "70%"
        , onInput changeText
        ]
        []


viewAnswerMethod : SelectedAnswerMethod -> Bool -> msg -> (AnswerMethod -> msg) -> Html msg
viewAnswerMethod selected expanded toggleMenu changeMethod =
    div
        [ style "visibility" (toggleVisibility expanded)
        , style "width" "20%"
        , style "height" "3rem"
        , style "border" "1px solid gray"
        , style "background" "rgb(235, 235, 235)"
        , style "margin" "0 0 0 2rem"
        , onClick toggleMenu
        ]
        [ viewAnswerMethodMenu selected changeMethod ]


viewDescription : String -> (String -> msg) -> Html msg
viewDescription description changeText =
    textarea
        [ placeholder "Description"
        , style "width" "70%"
        , style "overflow" "break-word"
        , onInput changeText
        ]
        [ text description ]


toggleVisibility : Bool -> String
toggleVisibility state =
    case state of
        True ->
            "visible"

        False ->
            "hidden"


viewAnswerMethodMenu : SelectedAnswerMethod -> (AnswerMethod -> msg) -> Html msg
viewAnswerMethodMenu menu select =
    case menu.menuOpen of
        False ->
            div [ style "margin" "1rem" ]
                [ text (getAnswerMethodName menu.selected) ]

        True ->
            div
                [ style "border" "1px solid gray"
                , style "z-index" "2000"
                , style "position" "sticky"
                ]
                [ viewMenuElement ShortAnswer
                    (ShortAnswer == menu.selected)
                    select
                , viewMenuElement Paragraph
                    (Paragraph == menu.selected)
                    select
                , viewMenuElement MultipleChoice
                    (MultipleChoice == menu.selected)
                    select
                , viewMenuElement CheckBox
                    (CheckBox == menu.selected)
                    select
                , viewMenuElement DropDown
                    (DropDown == menu.selected)
                    select
                ]


viewMenuElement : AnswerMethod -> Bool -> (AnswerMethod -> msg) -> Html msg
viewMenuElement method selected changeMethod =
    div
        [ onClick (changeMethod method)
        , style "padding" "1rem"
        , if selected then
            style "background" "rgb(215, 215, 215)"

          else
            style "background" "rgb(235, 235, 235)"
        ]
        [ text (getAnswerMethodName method) ]


getAnswerMethodName : AnswerMethod -> String
getAnswerMethodName type_ =
    case type_ of
        ShortAnswer ->
            "Short Answer"

        Paragraph ->
            "Paragraph"

        MultipleChoice ->
            "Multiple Choice"

        CheckBox ->
            "Checkbox"

        DropDown ->
            "Dropdown"


fieldFooter : Model -> (Bool -> msg) -> Html msg -> Html msg
fieldFooter model msg controls =
    div
        [ style "display" "flex"
        , style "justify-content" "right"
        ]
        [ controls
        , label []
            [ input
                [ type_ "checkbox"
                , checked model.required
                , onCheck msg
                ]
                []
            , text "Requited"
            ]
        ]


viewControls : Model -> Html msg -> Html msg
viewControls model footer =
    case model.expanded of
        False ->
            div [] []

        True ->
            div [ style "padding" "0 1rem 1rem 1rem" ]
                [ h1
                    []
                    [ text (getAnswerMethodName model.answerMethod.selected) ]
                , footer
                ]
