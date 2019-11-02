module MODEL exposing (..)


type alias SelectedAnswerMethod =
    { selected : AnswerMethod
    , menuOpen : Bool
    }



-- FIELD


type alias Field =
    { id : String
    , rootId : String
    , index : Int
    , question : String
    , description : String
    , answerMethod : SelectedAnswerMethod
    , required : Bool
    , expanded : Bool
    , status : Status
    }



-- FORM


type alias Form =
    { id : String
    , name : String
    , title : String
    , description : String
    , fields : List Field
    , status : Status
    }



-- OTHER


rootURL : String
rootURL =
    "http://127.0.0.1:5000/forms-json/"


type Status
    = Loading
    | Success
    | Failure


type AnswerMethod
    = ShortAnswer
    | Paragraph
    | MultipleChoice
    | CheckBox
    | DropDown


getAnswerMethodName : AnswerMethod -> String
getAnswerMethodName method =
    case method of
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
