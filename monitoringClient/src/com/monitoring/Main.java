package com.monitoring;

public class Main {

    static Monitor monitor = new Monitor();

    public static void main(String[] args)
    {
        monitor.start(args);               //set up this way for testing purposes
    }

    public static void setMonitor(Monitor monitor)
    {
        Main.monitor = monitor;
    }
}
