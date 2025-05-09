#ifndef __EVCHARGING_ELECTRICVEHICLE_H
#define __EVCHARGING_ELECTRICVEHICLE_H

#include <omnetpp.h>

class ElectricVehicle : public omnetpp::cSimpleModule
{
  private:
    int soc;                       // State of charge (integer percentage)
    int sendTime;                  // Integer to store send time
    int messageProcessedTime;      // Integer to store processed message time
    int chargeRequestCount;        // Integer for charge request count
    int energyConsumed;            // Integer for energy consumed
    int speed;                     // Integer for vehicle speed
    int lastEventTime;             // Integer for last event time

  protected:
    virtual void initialize() override;
    virtual void handleMessage(omnetpp::cMessage *msg) override;
};

#endif
