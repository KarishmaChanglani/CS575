package com.monitoring;

/**
 * Created by Patrick on 11/11/2016.
 */
public class Launcher
{
    public void start(String[] args)
    {
        if(args.length != 0 && args[0].equals("-s"))
            setup();
        standardRun();
    }

    public void setup()
    {
        
    }

    public void standardRun()
    {
    }
}
