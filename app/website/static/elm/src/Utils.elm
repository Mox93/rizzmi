module Utils exposing (..)

import Html exposing (Attribute)
import Html.Events exposing (on, targetValue)
import Json.Decode


onChange : (String -> msg) -> Attribute msg
onChange tagger =
    on "change" (Json.Decode.map tagger targetValue)
