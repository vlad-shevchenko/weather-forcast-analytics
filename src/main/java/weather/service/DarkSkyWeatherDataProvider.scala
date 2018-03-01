package weather.service

import java.util
import java.util.concurrent.CompletableFuture

import org.slf4j.{Logger, LoggerFactory}
import org.springframework.boot.context.properties.ConfigurationProperties
import org.springframework.stereotype.Service
import weather.domain.{ActualWeather, City, Forecast}

import scala.beans.BeanProperty

@Service
@ConfigurationProperties(prefix = "app.weather.dark-sky")
class DarkSkyWeatherDataProvider extends WeatherDataProvider {

  var logger: Logger = LoggerFactory.getLogger(classOf[DarkSkyWeatherDataProvider])

  @BeanProperty
  var apiKey: String = _

  override def getName: String = "DarkSky"

  override def getCurrentWeather(cities: util.Collection[City]): CompletableFuture[util.List[ActualWeather]] = {
    logger.info("DarkSky apiKey: {}", apiKey)
    throw new NotImplementedError()
  }

  override def getForecast(cities: util.Collection[City]): CompletableFuture[util.List[Forecast]] = {
    logger.info("DarkSky apiKey: {}", apiKey)
    throw new NotImplementedError()
  }
}