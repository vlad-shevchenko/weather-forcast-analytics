package weather.service

import java.util
import java.util.concurrent.CompletableFuture
import javax.annotation.PostConstruct

import org.joda.time._
import org.slf4j.{Logger, LoggerFactory}
import org.springframework.boot.context.properties.ConfigurationProperties
import org.springframework.stereotype.Service
import tk.plogitech.darksky.api.jackson.DarkSkyJacksonClient
import tk.plogitech.darksky.forecast._
import tk.plogitech.darksky.forecast.model.{Latitude, Longitude}
import weather.domain._

import scala.beans.BeanProperty
import scala.collection.JavaConversions._
import scala.collection.JavaConverters._
import scala.compat.java8.FutureConverters._
import scala.concurrent.ExecutionContext.Implicits.global
import scala.concurrent.Future

@Service
@ConfigurationProperties(prefix = "app.weather.dark-sky")
class DarkSkyWeatherDataProvider extends WeatherDataProvider {

  var logger: Logger = LoggerFactory.getLogger(classOf[DarkSkyWeatherDataProvider])

  @BeanProperty
  var apiKey: String = _

  var request: ForecastRequestBuilder = _
  var client: DarkSkyJacksonClient = _

  @PostConstruct
  def init(): Unit = {
    request = new ForecastRequestBuilder().key(new APIKey(apiKey))
    client = new DarkSkyJacksonClient()
  }

  override def getName: String = "DarkSky"

  override def getCurrentWeather(cities: util.Collection[City]): CompletableFuture[util.Collection[ActualWeather]] = {
    val dateTime = new DateTime(DateTimeZone.UTC)
    Future({
      cities.map(
        (city: City) => {
          val forecastRequest = request.location(new GeoCoordinates(new Longitude(city.getLongitude), new Latitude(city.getLatitude))).build()
          val currently = client.forecast(forecastRequest).getCurrently
          new ActualWeather(
            new WeatherKey(getName, city, dateTime),
            new WeatherData(currently.getTemperature + 273, currently.getHumidity, currently.getWindBearing.doubleValue(), currently.getWindSpeed)
          )
        }).toList.asJava.asInstanceOf[util.Collection[ActualWeather]]
    }).toJava.toCompletableFuture
  }

  override def getForecast(cities: util.Collection[City]): CompletableFuture[util.Collection[Forecast]] = {
    val dateTime = new DateTime(DateTimeZone.UTC)
    Future(cities.flatMap(city => {
      val forecastRequest = request.location(new GeoCoordinates(new Longitude(city.getLongitude), new Latitude(city.getLatitude))).build()
      val forecast = client.forecast(forecastRequest)
      forecast.getHourly.getData.asScala.map(dp => new Forecast(
        new ForecastKey(getName, city, new DateTime(dp.getTime.toEpochMilli, DateTimeZone.UTC), dateTime),
        new WeatherData(dp.getTemperature + 273, dp.getHumidity, dp.getWindBearing.doubleValue(), dp.getWindSpeed)
      ))
      // Daily forecast doesn't provide weather for specific time, but min and max values during the day. We don't support this as of now
//      forecast.getDaily.getData.asScala
//        .filter(dp => new Duration(new DateTime(DateTimeZone.UTC), new DateTime(dp.getTime, DateTimeZone.UTC)).isLongerThan(Duration.standardDays(2)))
//        .map(dp => new Forecast(
//          new ForecastKey(getName, city, new DateTime(dp.getTime, DateTimeZone.UTC), new DateTime),
//          new WeatherData(dp.getApparentTemperatureMax, dp.getHumidity, dp.getWindBearing.doubleValue(), dp.getWindSpeed)
//      ))
    }).toList.asJava.asInstanceOf[util.Collection[Forecast]]
    ).toJava.toCompletableFuture
  }
}