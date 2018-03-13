package weather.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RestController;
import weather.service.WeatherGatherService;

@RestController
public class MainController {

    private WeatherGatherService weatherGatherService;

    @Autowired
    public MainController(WeatherGatherService weatherGatherService) {
        this.weatherGatherService = weatherGatherService;
    }

    @RequestMapping(method = RequestMethod.POST, path = "/gather_weather_data_now")
    public void gatherWeatherDataNow() {
        weatherGatherService.gatherWeatherData();
    }

}
