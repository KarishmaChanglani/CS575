package com.monitoring;

import org.hyperic.sigar.DiskUsage;

/**
 * Created by Patrick on 12/5/2016.
 */
public class DiskIOSensor implements SystemSensor
{
    public static final String LABEL = "disk_usage";

    @Override
    public String getLabel()
    {
        return LABEL;
    }

    @Override
    public String getData()
    {
        DiskUsage du = new DiskUsage();
        String rv = String.format("%d",du.getReads()+du.getWrites());
        return rv;
    }
}
