package evcharging;

network EVChargingSim
{
    submodules:
        EV: ElectricVehicle;
        CS: ChargingStation;
        Grid: Grid;
        CMS: CentralManagementSystem;

    connections allowunconnected:
      EV.out --> CS.evIn;      // EV to Charging Station (EV to CS)
        CS.out --> Grid.in;      // Charging Station to Grid (Power request)
        CS.cmpOut --> CMS.in;    // Charging Station to CMS (Request to CMS)
        CMS.out --> CS.cmsIn;    // CMS to Charging Station (Authentication Response)
        Grid.out --> CS.gridIn; 
}