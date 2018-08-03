public class Product {
    private int id;
    private String name;

    public Product(int id, String name){
        this.id = id;
        this.name = name;
    }
}
Product p1 = new Product(1,"ABC");
Product p2 = new Product(1,"ABC");

System.out.println(p1 == p2);
System.out.println(p1.equals(p2));
