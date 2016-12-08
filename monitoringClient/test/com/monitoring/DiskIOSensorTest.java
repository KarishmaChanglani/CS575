package com.monitoring;

import org.junit.Assert;
import org.junit.Test;

/**
 * Created by Patrick on 12/8/2016.
 */
public class DiskIOSensorTest {
    @Test
    public void getLabel() throws Exception
    {
        DiskIOSensor diskIOSensor = new DiskIOSensor();

        Assert.assertEquals(diskIOSensor.getLabel(), DiskIOSensor.LABEL);
    }

    @Test
    public void getData() throws Exception
    {
        DiskIOSensor diskIOSensor = new DiskIOSensor();

        Assert.assertTrue(diskIOSensor.getData().matches("\\d+"));
    }

}