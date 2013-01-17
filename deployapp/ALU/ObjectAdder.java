
package ALU;

import java.io.*;

public class ObjectAdder {

	public static void main(String args[]) {

		if(args.length != 1) {
			System.err.println("You need to pass " +
				"an object name as an argument");
			System.exit(1);
		}

		int sum = 0;

		try {
			// download object from bucket
			Runtime.getRuntime().exec("picloud bucket get " + args[0] + " .").waitFor();
		} catch (IOException e) {
			System.err.println("Could not download object");
			System.exit(1);
		} catch (InterruptedException e) {
			System.err.println("Could not download object");
			System.exit(1);
		}

		try {
			// open file and sum numbers
			BufferedReader in = new BufferedReader(new FileReader(args[0]));
			String line;
			while ((line = in.readLine()) != null) {
				sum += Integer.parseInt(line);
			}
			in.close();
	
			// print sum to stdout
			System.out.println(Integer.toString(sum));

			System.exit(0);

		} catch (IOException e) {

			System.err.println("Error reading file");
			System.exit(1);

		}

	}

}
