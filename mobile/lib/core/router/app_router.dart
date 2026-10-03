import 'package:go_router/go_router.dart';
import '../../screens/home/home_screen.dart';
import '../../screens/requests/request_screen.dart';
import '../../screens/settings/settings_screen.dart';
final appRouter=GoRouter(routes:[GoRoute(path:'/',builder:(_,__)=>const HomeScreen()),GoRoute(path:'/requests',builder:(_,__)=>const RequestScreen()),GoRoute(path:'/settings',builder:(_,__)=>const SettingsScreen())]);
