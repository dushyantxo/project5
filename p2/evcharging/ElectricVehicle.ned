package evcharging;

simple ElectricVehicle
{
    parameters:
        int initialSOC = default(50); // State of charge in percent
        @display("i=block/cogwheel");
    gates:
        output out;
}
