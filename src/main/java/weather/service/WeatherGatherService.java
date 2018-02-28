package weather.service;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import javax.persistence.EntityManager;
import java.util.ArrayList;
import java.util.List;

@Service
@ConfigurationProperties(prefix = "app.weather")
public class WeatherGatherService {

    private static final Logger logger = LoggerFactory.getLogger(WeatherGatherService.class);

    private List<WeatherDataProvider> weatherDataProviders;
    private EntityManager entityManager;
    private List<String> cities = new ArrayList<>();

    @Autowired
    public WeatherGatherService(List<WeatherDataProvider> weatherDataProviders, EntityManager entityManager) {
        this.weatherDataProviders = weatherDataProviders;
        this.entityManager = entityManager;
    }

    @Scheduled(fixedRateString = "PT1M")
    @Transactional // TODO vlad: I'm not sure whether @Transactional works with futures (it most likely does not)
    public void gatherWeatherData() {
        logger.info("Initiating gathering weather data. Cities: {}", cities.toString());
        weatherDataProviders.forEach(wdp -> {
            logger.info("Gathering weather data using {}", wdp.getClass().getName());
            wdp.getCurrentWeather(cities).thenAccept(list -> list.forEach(entityManager::persist));
            wdp.getForecast(cities).thenAccept(list -> list.forEach(entityManager::persist));
        });
    }


    public List<String> getCities() {
        return cities;
    }
}
