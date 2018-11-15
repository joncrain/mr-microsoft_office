<?php 

/**
 * Microsoft_office class
 *
 * @package munkireport
 * @author joncrain
 **/
class Microsoft_office_controller extends Module_controller
{
	
	/*** Protect methods with auth! ****/
	function __construct()
	{
		// Store module path
		$this->module_path = dirname(__FILE__);
	}
	
  /**
 * Get microsoft_office information for serial_number
 *
 * @param string $serial serial number
 **/
public function get_data($serial_number = '')
{
      $obj = new View();
      if( ! $this->authorized())
      {
          $obj->view('json', array('msg' => 'Not authorized'));
          return;
      }

      $microsoft_office = new microsoft_office_model($serial_number);
      $obj->view('json', array('msg' => $microsoft_office->rs));
}

} // END class default_module
