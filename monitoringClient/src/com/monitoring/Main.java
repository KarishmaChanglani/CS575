package com.monitoring;

public class Main {

    static Launcher launcher = new Launcher();

    public static void main(String[] args)
    {
        launcher.start(args);               //set up this way for testing purposes
    }

    public static void setLauncher(Launcher launcher)
    {
        Main.launcher = launcher;
    }
}
