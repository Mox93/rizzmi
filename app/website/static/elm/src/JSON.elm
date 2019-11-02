module JSON exposing (..)

import Json.Decode as JD exposing (Decoder, andThen, bool, int, list, string)
import Json.Decode.Pipeline exposing (hardcoded, optional, required)
import Json.Encode as JE exposing (Value)
import MODEL exposing (..)



-- FIELD


fieldEncoder : Field -> Value
fieldEncoder field =
    JE.object
        [ ( "index", JE.int field.index )
        , ( "question", JE.string field.question )
        , ( "description", JE.string field.description )
        , ( "required", JE.bool field.required )
        , ( "input_type"
          , field.answerMethod.selected
                |> getAnswerMethodName
                |> JE.string
          )
        ]


fieldDecoder : Decoder Field
fieldDecoder =
    JD.succeed Field
        |> required "_id" string
        |> required "connection" string
        |> required "index" int
        |> optional "question" string ""
        |> optional "description" string ""
        |> required "input_type" answerMethodDecoder
        |> optional "required" bool False
        |> hardcoded False
        |> hardcoded Success


answerMethodDecoder : Decoder SelectedAnswerMethod
answerMethodDecoder =
    string
        |> andThen
            (\method ->
                case method of
                    "Short Answer" ->
                        JD.succeed <| SelectedAnswerMethod ShortAnswer False

                    "Paragraph" ->
                        JD.succeed <| SelectedAnswerMethod Paragraph False

                    "Multiple Choice" ->
                        JD.succeed <| SelectedAnswerMethod MultipleChoice False

                    "Checkbox" ->
                        JD.succeed <| SelectedAnswerMethod CheckBox False

                    "Dropdown" ->
                        JD.succeed <| SelectedAnswerMethod DropDown False

                    _ ->
                        JD.succeed <| SelectedAnswerMethod ShortAnswer False
            )



-- FORM


formMainInfoEncoder : Form -> Value
formMainInfoEncoder form =
    JE.object
        [ ( "name", JE.string form.name )
        , ( "title", JE.string form.title )
        , ( "description", JE.string form.description )
        ]


formDecoder : Decoder Form
formDecoder =
    JD.succeed Form
        |> required "_id" string
        |> required "name" string
        |> required "title" string
        |> required "description" string
        |> required "fields" (list fieldDecoder)
        |> hardcoded Success
