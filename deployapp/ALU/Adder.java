
package ALU;

public class Adder {

	public static void main(String args[]) {

		if(args.length != 2) {
			System.err.println("You need to pass " +
				"two arguments to be added");
			System.exit(1);
		}

		int x = Integer.parseInt(args[0]);
		int y = Integer.parseInt(args[1]);
		System.out.println(Integer.toString(x + y));

		System.exit(0);
	}

}
