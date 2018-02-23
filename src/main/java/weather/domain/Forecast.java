package weather.domain;

import javax.persistence.EmbeddedId;
import javax.persistence.Entity;
import javax.persistence.ManyToOne;

@Entity
public class Forecast {

    @EmbeddedId
    private ForecastKey key;

    @ManyToOne(optional = true)
    private ActualWeather actualWeather;

    private WeatherData data;

    public Forecast() {
    }

    public Forecast(ForecastKey key, WeatherData data) {
        this.key = key;
        this.data = data;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;

        Forecast forecast = (Forecast) o;

        if (!key.equals(forecast.key)) return false;
        return data.equals(forecast.data);
    }

    @Override
    public int hashCode() {
        int result = key.hashCode();
        result = 31 * result + data.hashCode();
        return result;
    }

    public ForecastKey getKey() {
        return key;
    }

    public ActualWeather getActualWeather() {
        return actualWeather;
    }

    public WeatherData getData() {
        return data;
    }

    public void setActualWeather(ActualWeather actualWeather) {
        this.actualWeather = actualWeather;
    }

}
