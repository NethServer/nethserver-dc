<?php

/* @var $view \Nethgui\Renderer\Xhtml */

echo $view->header()->setAttribute('template', $T('DomainController_Title'));

if($view['nsdcStatus'] === 'enabled'):
    $globalFlags = $view::STATE_DISABLED | $view::STATE_READONLY;
else:
?>
<div class='dcalert'>
  <p><?php echo $T('help_intro_label') ?></p>
  <p><?php echo $T('help_conditions_label') ?></p>
  <ul>
    <li><?php echo $T('help_condition1_label') ?></li>
    <li><?php echo $T('help_condition2_label') ?></li>
    <li><?php echo $T('help_condition3_label') ?></li>
  </ul>
</div>
<?php
endif;

echo $view->panel()
        ->insert($view->textInput('IpAddress', $globalFlags))
        ->insert($view->checkBox('force', 'yes', $globalFlags))
;

echo $view->textInput('NetbiosDomain', $view::STATE_DISABLED | $view::STATE_READONLY);

echo $view->buttonList($view::BUTTON_HELP)
    ->insert($view->button('StartDc', $view::BUTTON_SUBMIT | $globalFlags))
;

$view->includeCss("
    .dcalert {
        color: #222222;
        background-color: #EEEEEE;
        border: 1px solid #949494;
        border-radius: 2px;
        padding: 15px;
        margin: 10px;
    }

    .dcalert p {
        margin-bottom: 10px;
    }

    .dcalert ul {
        list-style-type: disc;
        margin-left: 25px;
    }
");

$adminTodoString = json_encode($view->getModuleUrl('/AdminTodo?notifications'), TRUE);

$view->includeJavascript("
(function ( $ ) {

    function loadPage() {
        $.Nethgui.Server.ajaxMessage({
            isMutation: false,
            url: $adminTodoString
        });
    }

    $(document).ready(function() {
        loadPage();
    });

})( jQuery);
");
