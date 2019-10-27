module Main exposing (..)

import Browser
import Html exposing (..)
import Html.Attributes exposing (..)
import Html.Events exposing (..)



-- MAIN


main =
    Browser.sandbox
        { init = init
        , update = update
        , view = view
        }



-- MODEL


type alias Card =
    { title : String
    , description : String
    , expanded : Bool
    }


type alias Model =
    { a : Card
    , b : Card
    , c : Card
    }


init : Model
init =
    { a = Card "Title 1" "Description" True
    , b = Card "Title 2" "Description" False
    , c = Card "Title 3" "Description" False
    }



-- UPDATE


type Msg
    = ShowA
    | ShowB
    | ShowC


update : Msg -> Model -> Model
update msg model =
    case msg of
        ShowA ->
            { model | a = expand model.a, b = collapse model.b, c = collapse model.c }

        ShowB ->
            { model | b = expand model.b, a = collapse model.a, c = collapse model.c }

        ShowC ->
            { model | c = expand model.c, a = collapse model.a, b = collapse model.b }


expand : Card -> Card
expand card =
    Card card.title card.description True


collapse : Card -> Card
collapse card =
    Card card.title card.description False



-- VIEW


view : Model -> Html Msg
view model =
    div
        [ style "width" "25rem" ]
        [ viewCard model.a ShowA
        , viewCard model.b ShowB
        , viewCard model.c ShowC
        ]


viewCard : Card -> msg -> Html msg
viewCard card toggle =
    div
        [ style "margin" "10px"
        , style "padding" "0 0 0 10px"
        , style "border" "1px solid gray"
        , style "background" (background card.expanded)
        , style "border-radius" "10px"
        , onClick toggle
        ]
        [ h2 [] [ text card.title ]
        , p
            [ style "display" (display card.expanded)
            , style "height" "5rem"
            ]
            [ text card.description ]
        ]


display : Bool -> String
display selected =
    if selected then
        "block"

    else
        "none"


background : Bool -> String
background selected =
    if selected then
        "#5BA50B"

    else
        "#DFFFBD"
