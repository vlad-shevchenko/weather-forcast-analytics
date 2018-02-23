package weather.domain;

import javax.persistence.EmbeddedId;
import javax.persistence.Entity;
import javax.persistence.OneToMany;
import java.util.HashSet;
import java.util.Set;

@Entity
public class ActualWeather {

    @EmbeddedId
    private WeatherKey key;

    private WeatherData data;

    @OneToMany
    private Set<Forecast> forecasts;

    public ActualWeather() {
    }

    public ActualWeather(WeatherKey key, WeatherData data) {
        this.key = key;
        this.data = data;
        forecasts = new HashSet<>();
    }

    public WeatherKey getKey() {
        return key;
    }

    public WeatherData getData() {
        return data;
    }

    public Set<Forecast> getForecasts() {
        return forecasts;
    }
}
