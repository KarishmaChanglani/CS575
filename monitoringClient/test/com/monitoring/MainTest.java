package com.monitoring;

import org.junit.Assert;
import org.junit.Test;
import org.junit.Assert.*;
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
        Launcher launcher = Mockito.mock(Launcher.class);
        Main.setLauncher(launcher);
        String[] args = new String[0];

        Main.main(args);

        verify(launcher).start(args);
    }

    @Test
    public void setLauncher_sets_Launcher()
    {
        Launcher launcher = new Launcher();

        Main.setLauncher(launcher);

        Assert.assertSame(Main.launcher, launcher);
    }
}