package weather;

import org.joda.time.DateTime;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.test.context.junit4.SpringRunner;

import static org.junit.Assert.assertEquals;

@RunWith(SpringRunner.class)
@SpringBootTest
public class DateTimeUtilsTests {

    @Configuration
    public static class Config {
        @Bean
        public DateTimeUtils dateTimeUtils() {
            return new DateTimeUtils();
        }
    }

    @Autowired
    private DateTimeUtils dateTimeUtils;

	@Test
	public void truncateRemovedInsignificantFields() {
        DateTime now = new DateTime();

        DateTime truncated = dateTimeUtils.truncateToHour(now);

        assertEquals(now.toLocalDate(), truncated.toLocalDate());
        assertEquals(now.getHourOfDay(), truncated.getHourOfDay());
        assertEquals(0, truncated.getMinuteOfHour());
        assertEquals(0, truncated.getSecondOfMinute());
        assertEquals(0, truncated.getMillisOfSecond());
    }

}
