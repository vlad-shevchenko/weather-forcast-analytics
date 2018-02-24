package weather.domain;

import org.joda.time.DateTime;
import org.joda.time.Period;

public class ForecastErrors {

    public String city;
    public String wdpName;
    public DateTime dateTime;
    public Period forecastPeriod;

    public WeatherData actualDate;
    public WeatherData forecastData;

    public ForecastErrors() {
    }

    public ForecastErrors(String city, String wdpName, DateTime dateTime, DateTime forecastCreationTime, WeatherData actualDate, WeatherData forecastData) {
        this.city = city;
        this.wdpName = wdpName;
        this.dateTime = dateTime;
        this.forecastPeriod = new Period(dateTime, forecastCreationTime);
        this.actualDate = actualDate;
        this.forecastData = forecastData;
    }

}
