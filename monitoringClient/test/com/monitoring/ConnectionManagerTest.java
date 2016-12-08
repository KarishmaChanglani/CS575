package com.monitoring;

import org.junit.Assert;
import org.junit.Test;

/**
 * Created by Patrick on 12/8/2016.
 */
public class ConnectionManagerTest {
    @Test
    public void addSensorData() throws Exception
    {
        ConnectionManager con = new ConnectionManager("URL", "ID");
        String key = "sensorLabel";
        String value = "sensorData";

        con.addSensorData(key, value);

        Assert.assertEquals(con.getNextPostData().get("category"), key);
        Assert.assertEquals(con.getNextPostData().get("data"), value);
    }

    @Test
    public void addKeyValue() throws Exception
    {
        ConnectionManager con = new ConnectionManager("URL", "ID");
        String key = "someKey";
        String value = "someValue";

        con.addKeyValue(key, value);

        Assert.assertEquals(con.getNextPostData().get(key), value);
    }
}