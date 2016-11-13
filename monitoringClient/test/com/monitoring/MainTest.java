package com.monitoring;

import org.junit.Assert;
import org.junit.Test;
import org.mockito.Mockito;
import static org.mockito.Mockito.*;

/**
 * Created by Patrick on 11/11/2016.
 */
public class MainTest
{
    @Test
    public void main_calls_launcher_start()
    {
        Monitor monitor = Mockito.mock(Monitor.class);
        Main.setMonitor(monitor);
        String[] args = new String[0];

        Main.main(args);

        verify(monitor).start(args);
    }

    @Test
    public void setLauncher_sets_Launcher()
    {
        Monitor monitor = new Monitor();

        Main.setMonitor(monitor);

        Assert.assertSame(Main.monitor, monitor);
    }
}