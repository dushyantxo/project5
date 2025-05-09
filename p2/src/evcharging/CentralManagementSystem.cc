#include <omnetpp.h>
using namespace omnetpp;

class CentralManagementSystem : public cSimpleModule {
protected:
    virtual void handleMessage(cMessage *msg) override {
        EV << "CMS received: " << msg->getName() << "\n";

        if (strcmp(msg->getName(), "AuthenticationRequest") == 0) {
            EV << "Sending back AuthenticationResponse\n";
            cMessage *resp = new cMessage("AuthenticationResponse");
            send(resp, "out");  // Send response back to CS
        }
        delete msg;
    }
};

Define_Module(CentralManagementSystem);
