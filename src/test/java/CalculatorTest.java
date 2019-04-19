import static org.junit.Assert.assertEquals;
import org.junit.Test;
import org.junit.Before;
import org.junit.After;

public class CalculatorTest{

	private Calculator cal;

	@Before
	public void setUp(){
		cal = new Calculator();
	}

	@After
	public void tearDown(){
		cal = null;
	}

	@Test
	public void testAdd(){
		assertEquals(cal.add(2,3), 5);
	}

	@Test
	public void testSub(){
		assertEquals(cal.sub(2,3), -1);
	}

	@Test
	public void testMul(){
		assertEquals(cal.mul(2,3), 6);
	}

	@Test
	public void testDiv(){
		assertEquals(cal.div(2,3), 0);
	}

	@Test(expected = IllegalArgumentException.class)
	public void testDivWithException(){
		cal.div(2,0);
	}

}
