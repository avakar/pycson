    ws <- [ \t]*
    nl <- (ws ('#' [^\n]*)? '\r'? '\n')+
    ews <- nl? ws

    null <- 'null'
    bool <- 'false' / 'true'
    number <- '0b'[01]+ / '0o'[0-7]+ / 0x[0-9a-fA-F]+
        / -?([1-9][0-9]* / '0')?'.'[0-9]+('e'[+-]?[0-9]+)?
        / -?([1-9][0-9]* / '0')('.'[0-9]+)?('e'[+-]?[0-9]+)?
    string <-
        "'" !"''" string_tail{X="'"} /
        "'''" string_tail{X="'''"} /
        '"' !'""' string_tail{X='""'} /
        '"""' string_tail{X='"""'}
    string_tail <- (!X (. / '\\'.))* X
    id <- [$a-zA-Z_][$0-9a-zA-Z_]*

    array <-
        '[' (array_value (ews ',' array_value / nl (object / ews simple_value))* (ews ',')?)?{I=} ews ']'
    array_value <- nl object / ws line_object / ews simple_value

    flow_kv <- (id / string) ews ':'
        (nl object / ws line_object / ews simple_value)
    flow_object <- '{' ews (flow_kv ews (',' ews flow_kv ews)* (',' ews)?)?{I=} '}'

    simple_value <- null / bool / number / string / array / flow_object

    line_kv <- (id / string) ws ':' ws
        (nl I indented_object / line_object / simple_value / nl I [ \t] ws simple_value)
    line_object <- line_kv (ws ',' ws line_kv)*?

    object <- ' ' object{I=I ' '} / '\t' object{I=I '\t'} / line_object (ws ','? nl I line_object)*
    indented_object <- ' ' object{I=I ' '} / '\t' object{I=I '\t'}

    root=nl? (object{I=} ws ','? / ws simple_value) ews !.
