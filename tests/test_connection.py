from connection import Connection
from unittest import mock


def test_get_all():
    with mock.patch('connection.Connection.get_printer', return_value={"error": "Printer is not operational"}):
        con = Connection("http://localhost", "fake_api_key")
        assert con.get_all() == {'elapsed_time': 'N/A','printer_status': 'Printer not operational', 'temp_bed': 'N/A', 'temp_nozzle': 'N/A'}

    with mock.patch('connection.Connection.get_printer', return_value={"sd":{"ready":"false"},"state":{"error":"","flags":
        {"cancelling":"false","closedOrError":"false","error":"false","finishing":"false","operational":"true",
         "paused":"false","pausing":"false","printing":"false","ready":"true","resuming":"false","sdReady":"false"},
        "text":"Operational"},"temperature":{"bed":{"actual":70.00,"offset":0,"target":0.0},
        "tool0":{"actual":230.00,"offset":0,"target":0.0}}}):
        con = Connection("http://localhost", "fake_api_key")
        assert con.get_all() == {'elapsed_time': 'N/A', 'printer_status': 'Printer Operational', 'temp_bed': 70.00,'temp_nozzle': 230.00}

    with mock.patch('connection.Connection.get_printer', return_value={"sd":{"ready":"false"},"state":{"error":"","flags":
        {"cancelling":"false","closedOrError":"false","error":"false","finishing":"false","operational":"true",
         "paused":"false","pausing":"false","printing":"true","ready":"true","resuming":"false","sdReady":"false"},
        "text":"Operational"},"temperature":{"bed":{"actual":70.00,"offset":0,"target":0.0},
        "tool0":{"actual":230.00,"offset":0,"target":0.0}}}):
        con = Connection("http://localhost", "fake_api_key")
        assert con.get_all() == {'elapsed_time': 'N/A', 'printer_status': 'Printing', 'temp_bed': 70.00,'temp_nozzle': 230.00}

