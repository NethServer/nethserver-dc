<?php

echo $view->header()->setAttribute('template', $T('DomainController_Title'));

echo $view->panel()
        ->insert($view->textInput('IpAddress'))
;

echo $view->buttonList($view::BUTTON_HELP)
    ->insert($view->button('StartDc', $view::BUTTON_SUBMIT))
;

