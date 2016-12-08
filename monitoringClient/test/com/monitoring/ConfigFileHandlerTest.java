package com.monitoring;

import org.junit.Assert;
import org.junit.Test;

import java.util.ArrayList;

/**
 * Created by Patrick on 11/28/2016.
 */
public class ConfigFileHandlerTest {
    @Test
    public void getMachineID_Returns_UUID_String() throws Exception
    {
        ConfigFileHandler config = new ConfigFileHandler();

        String result = config.getMachineID();
        String uuidRegex = "[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}";

        Assert.assertTrue(result.matches(uuidRegex));
    }

    @Test
    public void getURL_Returns_Valid_IPv4() throws Exception
    {
        ConfigFileHandler config = new ConfigFileHandler();

        String result = config.getURL();
        String ip = result.split(":")[0];
        String[] segments = ip.split(".");
        for(String s : segments)
            Assert.assertTrue(Integer.parseInt(s) <= 255);
    }

    @Test
    public void setURL() throws Exception
    {
        ConfigFileHandler config = new ConfigFileHandler();
        String testURL = "35.164.138.44:5678"; //Extremely broken: will overwrite entered config

        config.setURL(testURL);

        Assert.assertEquals(config.getURL(), testURL);
    }

    @Test
    public void getSensors() throws Exception
    {
        ConfigFileHandler config = new ConfigFileHandler();

        Assert.assertTrue(config.getSensors() instanceof ArrayList);
    }

    @Test
    public void addSensor_adds_item_to_getSensor_list() throws Exception    //not really a proper unit test
    {
        ConfigFileHandler config = new ConfigFileHandler();
        String testString = IPAddressSensor.LABEL;

        config.addSensor(testString);

        Assert.assertTrue(config.getSensors().contains(testString));
    }

}