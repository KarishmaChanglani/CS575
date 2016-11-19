package com.monitoring;

import java.net.InetAddress;
import java.net.UnknownHostException;

/**
 * Created by Patrick on 11/18/2016.
 */
public class IPAddressSensor implements SystemSensor
{
    private final String LABEL = "IPSENSOR";
    @Override
    public String getLabel()
    {
        return LABEL;
    }

    @Override
    public String getData()
    {
        String rv = "";
        try
        {
            rv = InetAddress.getLocalHost().toString();
            rv = rv.split("/")[1];                      //removes "MachineName/"
        }
        catch (Exception e){}

        return rv;
    }
}
