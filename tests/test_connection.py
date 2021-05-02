from connection import Connection
from pytest import fixture
from mock import Mock

# test Connection.get_all with defined return values Connection.get {"sd":{"ready":"false"},"state":{"error":"","flags":{"cancelling":"false","closedOrError":"false","error":"false","finishing":"false","operational":"true","paused":"false","pausing":"false","printing":"false","ready":"true","resuming":"false","sdReady":"false"},"text":"Operational"},"temperature":{"bed":{"actual":20.78,"offset":0,"target":0.0},"tool0":{"actual":21.37,"offset":0,"target":0.0}}}
AND  {"error":"Printer is not operational"}



