from piholeinflux import send_msg


def test_send_msg(mocker):
    """Test send_msg function, sending data to influxDB."""
    indata = {"some": "value", "gravity_last_updated": "should be gone"}
    expected = [
        {
            "measurement": "pihole",
            "tags": {"host": "myname"},
            "fields": {"some": "value", "ads_percentage_today": 0.0},
        }
    ]
    mock_influx = mocker.patch("influxdb.InfluxDBClient")

    send_msg(mock_influx(), indata, "myname")

    mock_influx().write_points.assert_called_once_with(expected)


def test_send_msg_integer(mocker):
    """Test proper conversion of ads_percentage_today to float."""

    def IsOfType(cls):
        class IsOfType(cls):
            def __eq__(self, other):
                return isinstance(other, cls)

        return IsOfType()

    """Test send_msg function, sending data to influxDB."""
    indata = {"ads_percentage_today": 0, "gravity_last_updated": "should be gone"}
    expected = [
        {
            "measurement": "pihole",
            "tags": {"host": "myname"},
            "fields": {"ads_percentage_today": IsOfType(float)},
        }
    ]
    mock_influx = mocker.patch("influxdb.InfluxDBClient")

    send_msg(mock_influx(), indata, "myname")

    mock_influx().write_points.assert_called_once_with(expected)
