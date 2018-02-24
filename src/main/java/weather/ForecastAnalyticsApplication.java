package weather;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.scheduling.annotation.EnableScheduling;

@SpringBootApplication
@EnableScheduling
public class ForecastAnalyticsApplication {

	public static void main(String[] args) {
		SpringApplication.run(ForecastAnalyticsApplication.class, args);
	}
	
}
