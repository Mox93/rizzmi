module HTTP exposing (..)

import Http exposing (Body)
import JSON exposing (..)
import MODEL exposing (..)



-- FIELD


sendFieldUpdate : String -> Body -> (Result Http.Error Field -> msg) -> Cmd msg
sendFieldUpdate url body msg =
    Http.post
        { url = url
        , body = body
        , expect = Http.expectJson msg fieldDecoder
        }



-- FORM


getFormTemplate : String -> (Result Http.Error Form -> msg) -> Cmd msg
getFormTemplate url msg =
    Http.get
        { url = url
        , expect = Http.expectJson msg formDecoder
        }


sendFormTemplate : String -> Body -> (Result Http.Error Form -> msg) -> Cmd msg
sendFormTemplate url body msg =
    Http.post
        { url = url
        , body = body
        , expect = Http.expectJson msg formDecoder
        }
