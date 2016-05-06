<?php

/* @var $view \Nethgui\Renderer\Xhtml */

echo $view->header()->setAttribute('template', $T('DomainController_Title'));

echo $view->panel()
        ->insert($view->textInput('IpAddress'))
        ->insert($view->checkBox('force', 'yes'))
;

echo $view->buttonList($view::BUTTON_HELP)
    ->insert($view->button('StartDc', $view::BUTTON_SUBMIT))
;

