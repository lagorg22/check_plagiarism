package store;
@WebServlet("/ShoppingCartServlet")
public class ShoppingCartServlet extends HttpServlet {
private static final long serialVersionUID = 1L;
public ShoppingCartServlet() {
super();
}
protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
}
protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
HttpSession session = request.getSession();
ShoppingCart sc = (ShoppingCart)session.getAttribute(ShoppingCart.SC_NAME);
ProductCatalog pc = (ProductCatalog)request.getServletContext().getAttribute(ProductCatalog.PC_NAME);
String id = request.getParameter("productID");
if (id != null) {
sc.addProduct(pc.getProduct(id), 1);
} else {
sc = new ShoppingCart();
Enumeration<String> enumeration = request.getParameterNames();
while (enumeration.hasMoreElements()) {
id = enumeration.nextElement();
sc.addProduct(pc.getProduct(id), Integer.parseInt(request.getParameter(id)));
}
session.setAttribute(ShoppingCart.SC_NAME, sc);
}
RequestDispatcher dispatch = request.getRequestDispatcher("shopping-cart.jsp");
dispatch.forward(request, response);
}
}