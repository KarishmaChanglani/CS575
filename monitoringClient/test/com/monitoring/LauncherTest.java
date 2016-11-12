package com.monitoring;

import org.junit.Before;
import org.junit.Test;

import static org.junit.Assert.*;
import static org.mockito.Mockito.spy;
import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;

/**
 * Created by Patrick on 11/11/2016.
 */
public class LauncherTest {

    Launcher launcher;

    @Before
    public void setup()
    {}

    @Test
    public void start_calls_setup_when_given_s_flag()
    {
        launcher = spy(new Launcher());
        String[] args = {"-s"};

        launcher.start(args);

        verify(launcher).setup();
    }

    @Test
    public void start_only_calls_standardRun_when_not_given_s_flag()
    {
        launcher = spy(new Launcher());
        String[] args = {};

        launcher.start(args);

        verify(launcher, times(0)).setup();
        verify(launcher).standardRun();
    }
}