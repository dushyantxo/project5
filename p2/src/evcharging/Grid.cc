#include <omnetpp.h>
using namespace omnetpp;

class Grid : public cSimpleModule {
protected:
    virtual void handleMessage(cMessage *msg) override {
        if (strcmp(msg->getName(), "PowerRequest") == 0) {
            EV << "Grid: Supplying power.\n";
        }
        delete msg;
    }
};

Define_Module(Grid);
