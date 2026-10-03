import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../models/radio_status.dart'; import '../services/api_service.dart';
final apiProvider=Provider((_)=>ApiService()); final radioProvider=FutureProvider<RadioStatus>((ref)=>ref.watch(apiProvider).radioStatus());
