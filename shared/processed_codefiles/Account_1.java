package login;
@WebServlet("/Account")
public class Account extends HttpServlet {
private static final long serialVersionUID = 1L;
public Account() {
super();
}
protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
}
protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
AccountManager am = (AccountManager)request.getServletContext().getAttribute(AccountManager.AM_NAME);
if(!am.hasAccount(request.getParameter("name"))){
am.createAccount(request.getParameter("name"), request.getParameter("pw"));
RequestDispatcher dispatch = request.getRequestDispatcher("welcome.jsp");
dispatch.forward(request, response);
} else {
RequestDispatcher dispatch = request.getRequestDispatcher("nameInUse.jsp");
dispatch.forward(request, response);
}
}
}