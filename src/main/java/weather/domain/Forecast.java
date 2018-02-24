package weather.domain;

import javax.persistence.EmbeddedId;
import javax.persistence.Entity;

@Entity
public class Forecast {

    @EmbeddedId
    private ForecastKey key;

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

    public WeatherData getData() {
        return data;
    }

}
