package com.monitoring;

import org.junit.Assert;
import org.junit.Test;

/**
 * Created by Patrick on 12/6/2016.
 */
public class IPAddressSensorTest {
    @Test
    public void getLabel() throws Exception
    {
        IPAddressSensor sensor = new IPAddressSensor();

        Assert.assertEquals(sensor.getLabel(), IPAddressSensor.LABEL);
    }

    @Test
    public void getData() throws Exception
    {
        IPAddressSensor sensor = new IPAddressSensor();

        Assert.assertTrue(sensor.getData() instanceof String);
    }

}