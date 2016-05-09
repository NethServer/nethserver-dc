<?php

namespace NethServer\Module;

/*
 * 
 * Copyright (C) 2016 Nethesis S.r.l.
 * http://www.nethesis.it - nethserver@nethesis.it
 *
 * This script is part of NethServer.
 *
 * NethServer is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License,
 * or any later version.
 *
 * NethServer is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with NethServer.  If not, see COPYING.
 */

use Nethgui\System\PlatformInterface as Validate;

class DomainController extends \Nethgui\Controller\AbstractController
{

    public function initialize()
    {
        parent::initialize();
        $this->declareParameter('IpAddress', $this->createValidator(Validate::IPv4), array('configuration', 'nsdc', 'IpAddress'));
        $this->declareParameter('force', '/^(yes)?$/');
    }

    public function bind(\Nethgui\Controller\RequestInterface $request)
    {
        parent::bind($request);
        $this->getValidator('IpAddress')->platform('dcipaddr', $this->parameters['force'] === 'yes' ? 1 : 0);
    }

    public function process()
    {
        parent::process();
        if($this->getRequest()->isMutation()) {
            $this->getPlatform()->getDatabase('configuration')->setProp('nsdc', array('status' => 'enabled'));
            $this->getPlatform()->signalEvent('nethserver-dc-save &');
        }
    }

    public function prepareView(\Nethgui\View\ViewInterface $view)
    {
        if ($this->getRequest()->isMutation()) {
            $this->getPlatform()->setDetachedProcessCondition('success', array(
                'location' => array(
                    'url' => $view->getModuleUrl('/DomainController?installSuccess'),
                    'freeze' => TRUE,
            )));
        }
        parent::prepareView($view);
        if($this->getRequest()->hasParameter('installSuccess')) {
            $view->getCommandList('/Main')->sendQuery($view->getModuleUrl('/Dashboard'));
        }
    }



}
