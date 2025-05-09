#include "ElectricVehicle.h"

Define_Module(ElectricVehicle);

void ElectricVehicle::initialize()
{
    // Read parameter from NED or ini file
    soc = par("initialSOC");
    EV << "Electric Vehicle initialized with SOC: " << soc << "%\n";

    // For demonstration, send a message to the next module
    omnetpp::cMessage *msg = new omnetpp::cMessage("EV_RequestCharge");
    send(msg, "out");
}

void ElectricVehicle::handleMessage(omnetpp::cMessage *msg)
{
    delete msg;
    EV << "Electric Vehicle received a message.\n";
}
