package weather.service;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Repository;
import weather.domain.ActualWeather;
import weather.domain.Forecast;
import weather.domain.ForecastErrors;

import javax.persistence.EntityManager;
import java.util.List;

@Repository
public class WeatherForecastAnalyticsService {

    private static final Logger logger = LoggerFactory.getLogger(WeatherForecastAnalyticsService.class);

    private final EntityManager entityManager;

    @Autowired
    public WeatherForecastAnalyticsService(EntityManager entityManager) {
        this.entityManager = entityManager;
    }

    public List<ForecastErrors> getForecastErrors() {
        return entityManager.createQuery("select new weather.domain.ForecastErrors(aw.key.city, aw.key.wdpName, aw.key.dateTime, f.key.forecastCreationTime, aw.data, f.data) from ActualWeather aw inner join Forecast f on aw.key.city = f.key.city and aw.key.wdpName = aw.key.wdpName and timestampdiff(second, aw.key.dateTime, f.key.forecastCreationTime) between -30 and 30", ForecastErrors.class)
                .getResultList();
    }
}
