package weather.domain;

import javax.persistence.EmbeddedId;
import javax.persistence.Entity;

@Entity
public class ActualWeather {

    @EmbeddedId
    private WeatherKey key;

    private WeatherData data;

    public ActualWeather() {
    }

    public ActualWeather(WeatherKey key, WeatherData data) {
        this.key = key;
        this.data = data;
    }

    public WeatherKey getKey() {
        return key;
    }

    public WeatherData getData() {
        return data;
    }

}
