package com.monitoring;

import org.junit.Before;
import org.junit.Test;
import org.mockito.Mockito;

import static org.mockito.Mockito.spy;
import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;

/**
 * Created by Patrick on 11/11/2016.
 */
public class MonitorTest {

    Monitor monitor;

    @Before
    public void setup()
    {}

    @Test
    public void start_calls_setup_when_given_s_flag()
    {
        monitor = spy(new Monitor());
        String[] args = {"-s"};

        monitor.start(args);

        verify(monitor).setup();
    }

    @Test
    public void start_only_calls_standardRun_when_not_given_s_flag()
    {
        monitor = spy(new Monitor());
        String[] args = {};
        ConnectionManager con = Mockito.mock(ConnectionManager.class);

        monitor.start(args);

        verify(monitor, times(0)).setup();
        verify(monitor).standardRun(con);
    }

}