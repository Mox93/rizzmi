module Main exposing (main)

import Bootstrap.CDN as CDN
import Bootstrap.Grid as Grid
import Bootstrap.Grid.Col as Col
import Bootstrap.Grid.Row as Row
import Html exposing (..)


main =
    Grid.container []
        [ CDN.stylesheet -- creates an inline style node with the Bootstrap CSS
        , Grid.row []
            [ Grid.col []
                [ text "Some content for my view here..." ]
            ]
        ]
